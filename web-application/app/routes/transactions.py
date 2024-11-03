from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from decimal import Decimal, InvalidOperation
from app.models import storage
from app.models.bank_account import BankAccount
from app.models.transaction import Transaction

transactions = Blueprint('transactions', __name__)


@transactions.route('/account/<int:account_id>/transactions')
@login_required
def account_transactions(account_id):
    """View full transaction history for an account"""
    account = storage.get_session().query(BankAccount).filter_by(
        id=account_id,
        user_id=current_user.id
    ).first()

    # Get all transactions for the account, ordered by date descending
    transactions = storage.get_session().query(Transaction).filter_by(
        account_id=account_id
    ).order_by(Transaction.transaction_date.desc()).all()

    return render_template(
        'accounts/account_detail.html',
        account=account,
        transactions=transactions
    )


@transactions.route('/account/<int:account_id>/transaction/new', methods=['GET', 'POST'])
@login_required
def new_transaction(account_id):
    """Handle creation of new transactions"""
    account = storage.get_session().query(BankAccount).filter_by(
        id=account_id,
        user_id=current_user.id
    ).first()

    if request.method == 'POST':
        try:
            # Get form data
            transaction_type = request.form.get('type')
            amount = Decimal(request.form.get('amount'))
            description = request.form.get('description')

            # Validate amount
            if amount <= 0:
                flash('Amount must be greater than zero.', 'error')
                return redirect(url_for('transactions.new_transaction', account_id=account_id))

            # Check sufficient funds for withdrawals
            if transaction_type == 'withdrawal' and amount > account.balance:
                flash('Insufficient funds for this withdrawal.', 'error')
                return redirect(url_for('transactions.new_transaction', account_id=account_id))

            # Calculate new balance
            new_balance = account.balance
            if transaction_type == 'deposit':
                new_balance += amount
            elif transaction_type == 'withdrawal':
                new_balance -= amount

            # Create transaction
            transaction = Transaction(
                account_id=account_id,
                transaction_type=transaction_type,
                amount=amount,
                description=description,
                transaction_date=datetime.now(),
                balance_after=new_balance
            )

            # Update account balance
            account.balance = new_balance

            # Save both the account and transaction
            transaction.save()
            account.save()

            flash('Transaction completed successfully.', 'success')
            return redirect(url_for('transactions.account_transactions', account_id=account_id))

        except (ValueError, InvalidOperation):
            flash('Please enter a valid amount.', 'error')
            return redirect(url_for('transactions.new_transaction', account_id=account_id))
        except Exception as e:
            storage.get_session().rollback()
            flash('An error occurred while processing the transaction.', 'error')
            return redirect(url_for('transactions.new_transaction', account_id=account_id))

    return render_template(
        'transactions/new_transaction.html',
        account=account
    )


@transactions.route('/transaction/<int:transaction_id>')
@login_required
def transaction_detail(transaction_id):
    """View details of a specific transaction"""
    # Join with account to ensure user owns this transaction
    transaction = storage.get_session().query(Transaction).join(BankAccount).filter(
        Transaction.id == transaction_id,
        BankAccount.user_id == current_user.id
    ).first_or_404()

    return render_template(
        'transaction_detail.html',
        transaction=transaction,
        account=transaction.account
    )
