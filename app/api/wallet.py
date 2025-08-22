from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.enums import TransactionType, TransactionStatus
from app.schemas.schemas import (
    FundsRequest, 
    TransactionResponse, 
    WalletBalanceResponse, 
    TransactionHistoryResponse,
    UserCreate,
    UserResponse,
    ErrorResponse
)
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wallet_api")

router = APIRouter()

@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        user = User(name=user_data.name)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created: {user.id}")
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.post("/addFunds", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def add_funds(data: FundsRequest, db: Session = Depends(get_db)):
    """Add funds to a user's wallet"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        # Get or create wallet
        wallet = db.query(Wallet).filter(Wallet.user_id == data.user_id).first()
        if not wallet:
            wallet = Wallet(user_id=data.user_id, balance=0.0)
            db.add(wallet)
            db.flush()  # Get wallet ID without committing
        
        # Update balance
        wallet.balance += data.amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=data.user_id,
            type=TransactionType.CREDIT,
            amount=data.amount,
            timestamp=datetime.utcnow(),
            status=TransactionStatus.SUCCESS,
            description=data.description or f"Added funds: ${data.amount}"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Funds added: ${data.amount} to user {data.user_id}")
        return transaction
        
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error adding funds: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing transaction"
        )

@router.post("/withdrawFunds", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def withdraw_funds(data: FundsRequest, db: Session = Depends(get_db)):
    """Withdraw funds from a user's wallet"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        # Check if wallet exists and has sufficient balance
        wallet = db.query(Wallet).filter(Wallet.user_id == data.user_id).first()
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Wallet not found"
            )
        
        if wallet.balance < data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient balance. Available: ${wallet.balance}, Requested: ${data.amount}"
            )
        
        # Update balance
        wallet.balance -= data.amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=data.user_id,
            type=TransactionType.DEBIT,
            amount=data.amount,
            timestamp=datetime.utcnow(),
            status=TransactionStatus.SUCCESS,
            description=data.description or f"Withdrew funds: ${data.amount}"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Funds withdrawn: ${data.amount} from user {data.user_id}")
        return transaction
        
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error withdrawing funds: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing transaction"
        )

@router.get("/balance/{user_id}", response_model=WalletBalanceResponse, status_code=status.HTTP_200_OK)
def get_balance(user_id: int, db: Session = Depends(get_db)):
    """Get wallet balance for a user"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        # Get wallet
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if not wallet:
            # Create wallet with zero balance if it doesn't exist
            wallet = Wallet(user_id=user_id, balance=0.0)
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
        
        return WalletBalanceResponse(wallet_id=wallet.id, balance=wallet.balance)
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error getting balance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving balance"
        )

@router.get("/transactions/{user_id}", response_model=TransactionHistoryResponse, status_code=status.HTTP_200_OK)
def get_transactions(user_id: int, limit: int = 100, db: Session = Depends(get_db)):
    """Get transaction history for a user"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        # Get transactions
        transactions = (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.timestamp.desc())
            .limit(limit)
            .all()
        )
        
        return TransactionHistoryResponse(
            user_id=user_id,
            transactions=transactions
        )
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error getting transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction history"
        )
