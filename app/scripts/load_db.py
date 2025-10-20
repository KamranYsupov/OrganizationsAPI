# utils/seed_from_json.py
import asyncio
import json
import uuid

import loguru
from dependency_injector.wiring import inject, Provide
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.db.manager import db_manager
from app.db.models import Building, Activity, Organization, Phone


async def seed_from_json():
    """
    Заполняет базу данных из JSON
    """
    async with db_manager.AsyncSessionLocal() as session:
        session = session

        with open('db_data.json', 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        buildings_map = {}
        for building_data in db_data["buildings"]:
            building = Building(
                id=building_data["id"],
                address=building_data["address"],
                latitude=building_data["latitude"],
                longitude=building_data["longitude"]
            )
            session.add(building)
            buildings_map[building_data["id"]] = building


        # 4. Создаем активности
        activities_map = {}
        for activity_data in db_data["activities"]:
            activity = Activity(
                id=activity_data["id"],
                name=activity_data["name"],
                parent_id=activity_data["parent_id"]
            )
            session.add(activity)
            activities_map[activity_data["id"]] = activity

        # 5. Создаем организации
        for org_data in db_data["organizations"]:
            organization = Organization(
                id=org_data["id"],
                name=org_data["name"],
                building_id=org_data["building_id"]
            )
            session.add(organization)

            # Добавляем связи с активностями
            for activity_id in org_data["activity_ids"]:
                if activity_id in activities_map:
                    organization.activities.append(activities_map[activity_id])


        for phone_data in db_data["phones"]:
            phone = Phone(
                id=phone_data["id"],
                number=phone_data["number"],
                organization_id=phone_data["organization_id"]
            )
            session.add(phone)

        await session.commit()


        loguru.logger.info(f"Загрузка выполнена успешно ✅")

        return True


if __name__ == "__main__":
    asyncio.run(seed_from_json())