import datetime
import getpass

from app.users.models import User
from app.users.service import hash_password
from app.database import async_session

import asyncio


async def main():
    print("Welcome to admin creator!")
    email = input("Email: ")
    fullname = input("Fullname: ")
    while True:
        try:
            print("Genders:\n0 - MALE\n1 - FEMALE\n2 - OTHER")
            gender = ["MALE", "FEMALE", "OTHER"][int(input("Gender: "))]
        except Exception:
            print("wrong number!")
            continue
        break
    while True:
        try:
            birthday = datetime.datetime.strptime(
                input("Bithday: (dd.mm.yyyy): "), "%d.%m.%Y"
            ).date()
        except Exception as e:
            print("wrong format!")
            continue
        break
    while True:
        p1 = getpass.getpass("Password: ").strip()
        p2 = getpass.getpass("Repeat password: ").strip()
        if p1 == p2:
            hashed_password = hash_password(p1)
            break
        else:
            print("Try again")
    async with async_session() as session:
        user = User(
            email=email,
            fullname=fullname,
            gender=gender,
            birthday=birthday,
            hashed_password=hashed_password,
        )
        session.add(user)
        await session.commit()
        print(f"admin successful created!\nID - {user.id}")


if __name__ == "__main__":
    asyncio.run(main())
