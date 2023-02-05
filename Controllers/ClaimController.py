from fastapi import HTTPException

from models.Claim import Claim

def getClaimById(db,id_claim):
    try :
        claim= db.query(Claim).filter(Claim.id == id_claim).first()
        return claim
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="Claim not found") 
    except Exception as e:    
        raise  HTTPException (status_code=500,detail="Error has been Occured")  


def add_Claim(claimDesription,db):
    try:
        if  claimDesription is None :
            raise ValueError("all fields are required") 
        claim=Claim(description=claimDesription)
    
        db.add(claim)
        db.commit()
        return "register succeded"
    except ValueError as ve:
     raise HTTPException(status_code=422,detail=str(ve))
    except Exception as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=500,detail="Error has been Occured") 


def removeClaim(db,id_claim):
    try :
         db.query(Claim).filter(Claim.id == id_claim).delete()
         db.commit()
         return "Claim Deleted"
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="Claim not found") 
    except Exception as e:    
        raise  HTTPException (status_code=500,detail="Error has been Occured")  


def update_Claim(id_claim,claimDesription,db):
    try:
        if  claimDesription is None :
            raise ValueError("No field updated") 
        
        
        claim=getClaimById(db,id_claim)
        
        claim.description=claimDesription
        db.commit()
        return "Claim Updated"
    except ValueError as ve:
     raise HTTPException(status_code=422,detail=str(ve))
    except Exception as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=500,detail="Error has been Occured ") 