# MODULES
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

# CONTEXTLIB
from contextlib import AbstractContextManager
from sqlalchemy import ColumnExpressionArgument

# SQLALCHEMY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, InstrumentedAttribute, Query

# DECORATORS
from session_repository.decorators import with_session

# UTILS
from session_repository.utils import (
    _FilterType,
    RelationshipOption,
    apply_distinct,
    apply_relationship_options,
    apply_filters,
    apply_order_by,
    apply_limit,
    apply_pagination,
)


_T = TypeVar("_T", bound=declarative_base())


class SessionRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
    ) -> None:
        self._session_factory = session_factory

    def session_manager(self):
        return self._session_factory()

    def _build_query(
        self,
        query: Query,
        model: Optional[Type[_T]] = None,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[Union[List[str], str]] = None,
        limit: int = None,
    ) -> Query:
        query = apply_relationship_options(
            query=query,
            relationship_options=relationship_options,
        )

        query = apply_filters(
            query=query,
            filter_dict=filters,
        )
        query = apply_filters(
            query=query,
            filter_dict=optional_filters,
            with_optional=True,
        )
        query = apply_order_by(
            query=query,
            model=model,
            order_by=order_by,
            direction=direction,
        )

        return apply_limit(
            query=query,
            limit=limit,
        )

    def _build_query_paginate(
        self,
        query: Query,
        model: Type[_T],
        page: int,
        per_page: int,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[Union[List[str], str]] = None,
        limit: int = None,
    ) -> Tuple[Query, str]:
        query = self._build_query(
            query=query,
            model=model,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
            order_by=order_by,
            direction=direction,
            limit=limit,
        )

        return apply_pagination(
            query=query,
            page=page,
            per_page=per_page,
        )

    @with_session()
    def _select(
        self,
        model: Type[_T],
        distinct: Optional[ColumnExpressionArgument] = None,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        session: Optional[Session] = None,
    ) -> Optional[_T]:
        query = apply_distinct(
            session=session,
            model=model,
            distinct=distinct,
        )

        return self._select_query(
            query=query,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
        )

    def _select_query(
        self,
        query: Query,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
    ) -> Optional[Any]:
        query = self._build_query(
            query=query,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
        )

        return query.first()

    @with_session()
    def _select_all(
        self,
        model: Type[_T],
        distinct: Optional[List[ColumnExpressionArgument]] = None,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[str] = None,
        limit: int = None,
        session: Optional[Session] = None,
    ) -> List[_T]:
        query = apply_distinct(
            session=session,
            model=model,
            distinct=distinct,
        )

        return self._select_all_query(
            query=query,
            model=model,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
            order_by=order_by,
            direction=direction,
            limit=limit,
        )

    def _select_all_query(
        self,
        query: Query,
        model: Type[_T],
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[Union[List[str], str]] = None,
        limit: int = None,
    ) -> List[_T]:
        query = self._build_query(
            query=query,
            model=model,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
            order_by=order_by,
            direction=direction,
            limit=limit,
        )

        return query.all()

    @with_session()
    def _select_paginate(
        self,
        model: Type[_T],
        page: int,
        per_page: int,
        distinct: Optional[ColumnExpressionArgument] = None,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[str] = None,
        limit: int = None,
        session: Optional[Session] = None,
    ) -> Tuple[List[_T], str]:
        query = apply_distinct(
            session=session,
            model=model,
            distinct=distinct,
        )

        return self._select_paginate_query(
            query=query,
            model=model,
            page=page,
            per_page=per_page,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
            order_by=order_by,
            direction=direction,
            limit=limit,
        )

    def _select_paginate_query(
        self,
        query: Query,
        model: Type[_T],
        page: int,
        per_page: int,
        filters: Optional[_FilterType] = None,
        optional_filters: Optional[_FilterType] = None,
        relationship_options: Optional[
            Dict[InstrumentedAttribute, RelationshipOption]
        ] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[str] = None,
        limit: int = None,
    ) -> Tuple[List[_T], str]:
        query, pagination = self._build_query_paginate(
            query=query,
            model=model,
            page=page,
            per_page=per_page,
            filters=filters,
            optional_filters=optional_filters,
            relationship_options=relationship_options,
            order_by=order_by,
            direction=direction,
            limit=limit,
        )

        return query.all(), pagination

    @with_session()
    def _update_all(
        self,
        model: Type[_T],
        values: Dict,
        filters: Optional[_FilterType] = None,
        flush: bool = False,
        commit: bool = False,
        session: Optional[Session] = None,
    ) -> List[_T]:
        rows = self._select_all(
            model=model,
            filters=filters,
            session=session,
        )

        if len(rows) == 0:
            return rows

        for row in rows:
            for key, value in values.items():
                setattr(row, key, value)

        if flush:
            session.flush()
        if commit:
            session.commit()

        [session.refresh(row) for row in rows]

        return rows

    @with_session()
    def _update(
        self,
        model: Type[_T],
        values: Dict,
        filters: Optional[_FilterType] = None,
        flush: bool = False,
        commit: bool = False,
        session: Optional[Session] = None,
    ) -> _T:
        row = self._select(
            model=model,
            filters=filters,
            session=session,
        )

        if row is None:
            return

        for key, value in values.items():
            setattr(row, key, value)

        if flush:
            session.flush()
        if commit:
            session.commit()

        session.refresh(row)

        return row

    @with_session()
    def _add_all(
        self,
        data: List[_T],
        flush: bool = False,
        commit: bool = False,
        session: Optional[Session] = None,
    ) -> List[_T]:
        session.add_all(data)
        if flush:
            session.flush()
        if commit:
            session.commit()

        if flush or commit:
            [session.refresh(item) for item in data]

        return data

    @with_session()
    def _add(
        self,
        data: _T,
        flush: bool = False,
        commit: bool = False,
        session: Optional[Session] = None,
    ) -> _T:
        session.add(data)
        if flush:
            session.flush()
        if commit:
            session.commit()

        if flush or commit:
            session.refresh(data)

        return data

    @with_session()
    def _delete(
        self,
        model: Type[_T],
        filters: Optional[_FilterType] = None,
        flush: bool = True,
        commit: bool = False,
        session: Optional[Session] = None,
    ) -> bool:
        rows: List = self._select_all(
            model=model,
            filters=filters,
            session=session,
        )

        if len(rows) == 0:
            return False

        for row in rows:
            session.delete(row)

        if flush:
            session.flush()
        if commit:
            session.commit()

        return True
