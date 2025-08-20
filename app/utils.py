from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


# hadi l function pour verifier les donne li rahom f database ida nfshom li dakhlhom l user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
