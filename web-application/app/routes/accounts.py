from flask import Blueprint, request, url_for, flash, redirect, render_template, current_app, jsonify
from flask_login import login_required, current_user
from app.models.bank_account import BankAccount
from app.models import storage
from sqlalchemy.exc import SQLAlchemyError

accounts = Blueprint('accounts', __name__)

@accounts.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    """Retrieve all accounts for the logged-in user."""
    accounts = current_user.bank_accounts
    return render_template('accounts/accounts.html', accounts=accounts)

@accounts.route('/accounts/<int:account_id>', methods=['GET'])
@login_required
def get_account(account_id):
    """Retrieve details of a specific account."""
    print(account_id)
    account = storage.get_session().query(BankAccount).filter_by(id=account_id).first()
    print(account)
    return render_template('accounts/account_detail.html', account=account)

@accounts.route('/accounts/new', methods=['GET', 'POST'])
@login_required
def create_account():
    """Create a new bank account."""
    if request.method == 'POST':
        account_number = request.form['accountNumber']
        account_type = request.form['accountType']
        new_account = BankAccount(user_id=current_user.id,
                                   account_number=account_number,
                                   account_type=account_type)
        new_account.save()
        flash('Account created successfully!', 'success')
        return redirect(url_for('accounts.get_accounts'))
    return render_template('accounts/create_account.html')

@accounts.route('/accounts/<int:account_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    """Edit an existing bank account."""
    account = storage.get(BankAccount, account_id)
    if request.method == 'POST':
        account.account_number = request.form['accountNumber']
        account.account_type = request.form['accountType']
        account.save()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('accounts.get_account', account_id=account.id))
    return render_template('accounts/edit_account.html', account=account)

@accounts.route('/accounts/delete/<int:account_id>', methods=['DELETE'])
@login_required
def delete_account(account_id):
    """Delete a specific bank account."""
    try:
        # Get the account
        account = storage.get(BankAccount, account_id)
        
        # Check if account exists
        if not account:
            return jsonify({
                'success': False,
                'message': 'Account not found'
            }), 404
            
        # Check if user owns this account
        if account.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access'
            }), 403

        # Check if account has zero balance before deletion
        if account.balance != 0:
            return jsonify({
                'success': False,
                'message': 'Cannot delete account with non-zero balance'
            }), 400

        # Perform the deletion
        account.delete()
        storage.save()

        return jsonify({
            'success': True,
            'message': 'Account deleted successfully!',
            'account_id': account_id
        }), 200

    except SQLAlchemyError as e:
        # Log the error (assuming you have proper logging set up)
        current_app.logger.error(f"Database error while deleting account {account_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting the account'
        }), 500
    
    except Exception as e:
        current_app.logger.error(f"Unexpected error while deleting account {account_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred'
        }), 500
