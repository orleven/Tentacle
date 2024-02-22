#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: orleven

import sqlite3
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.dialects.sqlite import insert
from lib.core.g import log
from lib.core.model import Vul
from lib.core.model import Task
from lib.util.util import get_time


async def sql_query(async_session, model, parser='to_json', condition=None, all_flag=True):
    """通用查询函数"""
    try:
        async with async_session.begin() as session:
            if condition is not None:
                stmt = select(model).where(condition)
            else:
                stmt = select(model)

            result = await session.execute(stmt)
            if all_flag:
                result = result.scalars().all()
                if result:
                    return [getattr(x, parser)() for x in result]
            else:
                result = result.scalars().first()
                if result:
                    return getattr(result, parser)()

    except Exception as e:
        msg = str(e)
        log.error(f"Error query, model: {model.__tablename__}, condition: {condition}, parser: {parser}, error: {msg}")
    return None


async def sql_delete(async_session, model, condition=None):
    """通用删除函数"""
    try:
        async with async_session.begin() as session:
            if condition is not None:
                stmt = delete(model).where(condition)
            else:
                stmt = select(model)
            await session.execute(stmt)
            return True
    except Exception as e:
        msg = str(e)
        log.error(f"Error delete, model: {model.__tablename__}, condition: {condition}, error: {msg}")
    return False

async def sql_save(async_session, model, data_list: list, key_update=None):
    """通用保存函数， 已存在则刷新key_update"""

    if key_update is None:
        key_update = {}

    try:
        async with async_session.begin() as session:
            # sqlite3 低版本不支持 on_conflict_do_update
            sqlite_version_nums = [int(num) for num in sqlite3.sqlite_version.split('.')]
            # required_version_nums = [3, 24, 0]
            required_version_nums = [3, 32, 0]
            if sqlite_version_nums >= required_version_nums:
                stmt = insert(model).values(data_list)
                stmt = stmt.on_conflict_do_update(set_=key_update)
                await session.execute(stmt)
                await session.commit()
            else:
                key_where_list = [key for key in dir(model) if hasattr(getattr(model, key), 'default') and (
                        getattr(model, key).primary_key or getattr(model, key).unique
                )]
                for data in data_list:
                    condition = (1 == 1)
                    for key in key_where_list:
                        if data.get(key, None):
                            condition = and_(condition, getattr(model, key) == data.get(key))
                    stmt = select(model).where(condition)
                    result = await session.execute(stmt)
                    result = result.scalars().all()
                    if result:
                        stmt = update(model).where(condition).values(key_update)
                        await session.execute(stmt)
                        await session.commit()
                    else:
                        stmt = insert(model).values([data])
                        await session.execute(stmt)
                        await session.commit()
    except Exception as e:
        msg = str(e)
        log.error(f"Error save, model: {model.__tablename__}, data_list: {data_list}, key_update: {key_update,}, error: {msg}")
    return False


async def sql_inject(async_session, model, data_list: list):
    """通用插入函数"""

    try:
        async with async_session.begin() as session:
            stmt = insert(model).values(data_list)
            await session.execute(stmt)
            await session.commit()
            return True
    except Exception as e:
        msg = str(e)
        log.error(f"Error inject, model: {model.__tablename__}, data_list: {data_list}, error: {msg}")
    return False


async def create_table(async_engine, model):
    """
    创建数据库、表结构
    :return:
    """
    # 初始化表结构
    async with async_engine.begin() as session:
        # await session.run_sync(model.metadata.drop_all)
        await session.run_sync(model.metadata.create_all)
        await session.commit()

async def inject_task(async_engine, task: dict):
    """保存task"""

    task_list = [task]
    return await sql_inject(async_engine, Task, task_list)


async def save_task(async_engine, task: dict, key_update=None):
    """保存task"""

    task_list = [task]

    if key_update is None:
        key_update = dict(update_time=get_time())

    return await sql_save(async_engine, Task, task_list, key_update)

async def save_data(async_engine, data: dict, data_model, key_update=None):
    """保存data"""

    data_list = [data]

    if key_update is None:
        key_update = dict(update_time=get_time())

    return await sql_save(async_engine, data_model, data_list, key_update)

async def query_vul(async_session):
    condition = and_(1 == 1)
    return await sql_query(async_session, model=Vul, parser="to_json", condition=condition, all_flag=False)

async def query_all_vul(async_session):
    condition = and_(1 == 1)
    return await sql_query(async_session, model=Vul, condition=condition, all_flag=True)
