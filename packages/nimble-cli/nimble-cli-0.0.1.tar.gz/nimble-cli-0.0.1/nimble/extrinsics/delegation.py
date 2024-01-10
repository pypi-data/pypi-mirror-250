# The MIT License (MIT)
# Copyright © 2024 Nimble Labs Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import nimble
from ..errors import *
from rich.prompt import Confirm
from typing import List, Dict, Union, Optional
from nimble.utils.balance import Balance
from .staking import __do_add_stake_single

from loguru import logger

logger = logger.opt(colors=True)


def nominate_extrinsic(
    nbnetwork: "nimble.nbnetwork",
    wallet: "nimble.wallet",
    wait_for_finalization: bool = False,
    wait_for_inclusion: bool = True,
) -> bool:
    r"""Becomes a delegate for the hotkey.
    Args:
        wallet ( nimble.wallet ):
            The wallet to become a delegate for.
    Returns:
        success (bool):
            True if the transaction was successful.
    """
    # Unlock the coldkey.
    wallet.coldkey
    wallet.hotkey

    # Check if the hotkey is already a delegate.
    if nbnetwork.is_hotkey_delegate(wallet.hotkey.ss58_address):
        logger.error(
            "Hotkey {} is already a delegate.".format(wallet.hotkey.ss58_address)
        )
        return False

    with nimble.__console__.status(
        ":satellite: Sending nominate call on [white]{}[/white] ...".format(
            nbnetwork.network
        )
    ):
        try:
            success = nbnetwork._do_nominate(
                wallet=wallet,
                wait_for_inclusion=wait_for_inclusion,
                wait_for_finalization=wait_for_finalization,
            )

            if success == True:
                nimble.__console__.print(
                    ":white_heavy_check_mark: [green]Finalized[/green]"
                )
                nimble.logging.success(
                    prefix="Become Delegate",
                    sufix="<green>Finalized: </green>" + str(success),
                )

            # Raises NominationError if False
            return success

        except Exception as e:
            nimble.__console__.print(
                ":cross_mark: [red]Failed[/red]: error:{}".format(e)
            )
            nimble.logging.warning(
                prefix="Set weights", sufix="<red>Failed: </red>" + str(e)
            )
        except NominationError as e:
            nimble.__console__.print(
                ":cross_mark: [red]Failed[/red]: error:{}".format(e)
            )
            nimble.logging.warning(
                prefix="Set weights", sufix="<red>Failed: </red>" + str(e)
            )

    return False


def delegate_extrinsic(
    nbnetwork: "nimble.nbnetwork",
    wallet: "nimble.wallet",
    delegate_ss58: Optional[str] = None,
    amount: Union[Balance, float] = None,
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
    prompt: bool = False,
) -> bool:
    r"""Delegates the specified amount of stake to the passed delegate.
    Args:
        wallet (nimble.wallet):
            nimble wallet object.
        delegate_ss58 (Optional[str]):
            ss58 address of the delegate.
        amount (Union[Balance, float]):
            Amount to stake as nimble balance, or float interpreted as Tao.
        wait_for_inclusion (bool):
            If set, waits for the extrinsic to enter a block before returning true,
            or returns false if the extrinsic fails to enter the block within the timeout.
        wait_for_finalization (bool):
            If set, waits for the extrinsic to be finalized on the chain before returning true,
            or returns false if the extrinsic fails to be finalized within the timeout.
        prompt (bool):
            If true, the call waits for confirmation from the user before proceeding.
    Returns:
        success (bool):
            flag is true if extrinsic was finalized or uncluded in the block.
            If we did not wait for finalization / inclusion, the response is true.

    Raises:
        NotRegisteredError:
            If the wallet is not registered on the chain.
        NotDelegateError:
            If the hotkey is not a delegate on the chain.
    """
    # Decrypt keys,
    wallet.coldkey
    if not nbnetwork.is_hotkey_delegate(delegate_ss58):
        raise NotDelegateError("Hotkey: {} is not a delegate.".format(delegate_ss58))

    # Get state.
    my_prev_coldkey_balance = nbnetwork.get_balance(wallet.coldkey.ss58_address)
    delegate_take = nbnetwork.get_delegate_take(delegate_ss58)
    delegate_owner = nbnetwork.get_hotkey_owner(delegate_ss58)
    my_prev_delegated_stake = nbnetwork.get_stake_for_coldkey_and_hotkey(
        coldkey_ss58=wallet.coldkeypub.ss58_address, hotkey_ss58=delegate_ss58
    )

    # Convert to nimble.Balance
    if amount == None:
        # Stake it all.
        staking_balance = nimble.Balance.from_tao(my_prev_coldkey_balance.tao)
    elif not isinstance(amount, nimble.Balance):
        staking_balance = nimble.Balance.from_tao(amount)
    else:
        staking_balance = amount

    # Remove existential balance to keep key alive.
    if staking_balance > nimble.Balance.from_rao(1000):
        staking_balance = staking_balance - nimble.Balance.from_rao(1000)
    else:
        staking_balance = staking_balance

    # Check enough balance to stake.
    if staking_balance > my_prev_coldkey_balance:
        nimble.__console__.print(
            ":cross_mark: [red]Not enough balance[/red]:[bold white]\n  balance:{}\n  amount: {}\n  coldkey: {}[/bold white]".format(
                my_prev_coldkey_balance, staking_balance, wallet.name
            )
        )
        return False

    # Ask before moving on.
    if prompt:
        if not Confirm.ask(
            "Do you want to delegate:[bold white]\n  amount: {}\n  to: {}\n owner: {}[/bold white]".format(
                staking_balance, delegate_ss58, delegate_owner
            )
        ):
            return False

    try:
        with nimble.__console__.status(
            ":satellite: Staking to: [bold white]{}[/bold white] ...".format(
                nbnetwork.network
            )
        ):
            staking_response: bool = nbnetwork._do_delegation(
                wallet=wallet,
                delegate_ss58=delegate_ss58,
                amount=staking_balance,
                wait_for_inclusion=wait_for_inclusion,
                wait_for_finalization=wait_for_finalization,
            )

        if staking_response == True:  # If we successfully staked.
            # We only wait here if we expect finalization.
            if not wait_for_finalization and not wait_for_inclusion:
                return True

            nimble.__console__.print(
                ":white_heavy_check_mark: [green]Finalized[/green]"
            )
            with nimble.__console__.status(
                ":satellite: Checking Balance on: [white]{}[/white] ...".format(
                    nbnetwork.network
                )
            ):
                new_balance = nbnetwork.get_balance(address=wallet.coldkey.ss58_address)
                block = nbnetwork.get_current_block()
                new_delegate_stake = nbnetwork.get_stake_for_coldkey_and_hotkey(
                    coldkey_ss58=wallet.coldkeypub.ss58_address,
                    hotkey_ss58=delegate_ss58,
                    block=block,
                )  # Get current stake

                nimble.__console__.print(
                    "Balance:\n  [blue]{}[/blue] :arrow_right: [green]{}[/green]".format(
                        my_prev_coldkey_balance, new_balance
                    )
                )
                nimble.__console__.print(
                    "Stake:\n  [blue]{}[/blue] :arrow_right: [green]{}[/green]".format(
                        my_prev_delegated_stake, new_delegate_stake
                    )
                )
                return True
        else:
            nimble.__console__.print(
                ":cross_mark: [red]Failed[/red]: Error unknown."
            )
            return False

    except NotRegisteredError as e:
        nimble.__console__.print(
            ":cross_mark: [red]Hotkey: {} is not registered.[/red]".format(
                wallet.hotkey_str
            )
        )
        return False
    except StakeError as e:
        nimble.__console__.print(":cross_mark: [red]Stake Error: {}[/red]".format(e))
        return False


def undelegate_extrinsic(
    nbnetwork: "nimble.nbnetwork",
    wallet: "nimble.wallet",
    delegate_ss58: Optional[str] = None,
    amount: Union[Balance, float] = None,
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
    prompt: bool = False,
) -> bool:
    r"""Un-delegates stake from the passed delegate.
    Args:
        wallet (nimble.wallet):
            nimble wallet object.
        delegate_ss58 (Optional[str]):
            ss58 address of the delegate.
        amount (Union[Balance, float]):
            Amount to unstake as nimble balance, or float interpreted as Tao.
        wait_for_inclusion (bool):
            If set, waits for the extrinsic to enter a block before returning true,
            or returns false if the extrinsic fails to enter the block within the timeout.
        wait_for_finalization (bool):
            If set, waits for the extrinsic to be finalized on the chain before returning true,
            or returns false if the extrinsic fails to be finalized within the timeout.
        prompt (bool):
            If true, the call waits for confirmation from the user before proceeding.
    Returns:
        success (bool):
            flag is true if extrinsic was finalized or uncluded in the block.
            If we did not wait for finalization / inclusion, the response is true.

    Raises:
        NotRegisteredError:
            If the wallet is not registered on the chain.
        NotDelegateError:
            If the hotkey is not a delegate on the chain.
    """
    # Decrypt keys,
    wallet.coldkey
    if not nbnetwork.is_hotkey_delegate(delegate_ss58):
        raise NotDelegateError("Hotkey: {} is not a delegate.".format(delegate_ss58))

    # Get state.
    my_prev_coldkey_balance = nbnetwork.get_balance(wallet.coldkey.ss58_address)
    delegate_take = nbnetwork.get_delegate_take(delegate_ss58)
    delegate_owner = nbnetwork.get_hotkey_owner(delegate_ss58)
    my_prev_delegated_stake = nbnetwork.get_stake_for_coldkey_and_hotkey(
        coldkey_ss58=wallet.coldkeypub.ss58_address, hotkey_ss58=delegate_ss58
    )

    # Convert to nimble.Balance
    if amount == None:
        # Stake it all.
        unstaking_balance = nimble.Balance.from_tao(my_prev_delegated_stake.tao)

    elif not isinstance(amount, nimble.Balance):
        unstaking_balance = nimble.Balance.from_tao(amount)

    else:
        unstaking_balance = amount

    # Check enough stake to unstake.
    if unstaking_balance > my_prev_delegated_stake:
        nimble.__console__.print(
            ":cross_mark: [red]Not enough delegated stake[/red]:[bold white]\n  stake:{}\n  amount: {}\n coldkey: {}[/bold white]".format(
                my_prev_delegated_stake, unstaking_balance, wallet.name
            )
        )
        return False

    # Ask before moving on.
    if prompt:
        if not Confirm.ask(
            "Do you want to un-delegate:[bold white]\n  amount: {}\n  from: {}\n  owner: {}[/bold white]".format(
                unstaking_balance, delegate_ss58, delegate_owner
            )
        ):
            return False

    try:
        with nimble.__console__.status(
            ":satellite: Unstaking from: [bold white]{}[/bold white] ...".format(
                nbnetwork.network
            )
        ):
            staking_response: bool = nbnetwork._do_undelegation(
                wallet=wallet,
                delegate_ss58=delegate_ss58,
                amount=unstaking_balance,
                wait_for_inclusion=wait_for_inclusion,
                wait_for_finalization=wait_for_finalization,
            )

        if staking_response == True:  # If we successfully staked.
            # We only wait here if we expect finalization.
            if not wait_for_finalization and not wait_for_inclusion:
                return True

            nimble.__console__.print(
                ":white_heavy_check_mark: [green]Finalized[/green]"
            )
            with nimble.__console__.status(
                ":satellite: Checking Balance on: [white]{}[/white] ...".format(
                    nbnetwork.network
                )
            ):
                new_balance = nbnetwork.get_balance(address=wallet.coldkey.ss58_address)
                block = nbnetwork.get_current_block()
                new_delegate_stake = nbnetwork.get_stake_for_coldkey_and_hotkey(
                    coldkey_ss58=wallet.coldkeypub.ss58_address,
                    hotkey_ss58=delegate_ss58,
                    block=block,
                )  # Get current stake

                nimble.__console__.print(
                    "Balance:\n  [blue]{}[/blue] :arrow_right: [green]{}[/green]".format(
                        my_prev_coldkey_balance, new_balance
                    )
                )
                nimble.__console__.print(
                    "Stake:\n  [blue]{}[/blue] :arrow_right: [green]{}[/green]".format(
                        my_prev_delegated_stake, new_delegate_stake
                    )
                )
                return True
        else:
            nimble.__console__.print(
                ":cross_mark: [red]Failed[/red]: Error unknown."
            )
            return False

    except NotRegisteredError as e:
        nimble.__console__.print(
            ":cross_mark: [red]Hotkey: {} is not registered.[/red]".format(
                wallet.hotkey_str
            )
        )
        return False
    except StakeError as e:
        nimble.__console__.print(":cross_mark: [red]Stake Error: {}[/red]".format(e))
        return False
