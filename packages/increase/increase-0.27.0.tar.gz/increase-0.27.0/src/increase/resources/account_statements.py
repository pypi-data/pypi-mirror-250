# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ..types import AccountStatement, account_statement_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..pagination import SyncPage, AsyncPage
from .._base_client import (
    AsyncPaginator,
    make_request_options,
)

__all__ = ["AccountStatements", "AsyncAccountStatements"]


class AccountStatements(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccountStatementsWithRawResponse:
        return AccountStatementsWithRawResponse(self)

    def retrieve(
        self,
        account_statement_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountStatement:
        """
        Retrieve an Account Statement

        Args:
          account_statement_id: The identifier of the Account Statement to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/account_statements/{account_statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountStatement,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        statement_period_start: account_statement_list_params.StatementPeriodStart | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPage[AccountStatement]:
        """
        List Account Statements

        Args:
          account_id: Filter Account Statements to those belonging to the specified Account.

          cursor: Return the page of entries after this one.

          limit: Limit the size of the list that is returned. The default (and maximum) is 100
              objects.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/account_statements",
            page=SyncPage[AccountStatement],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "cursor": cursor,
                        "limit": limit,
                        "statement_period_start": statement_period_start,
                    },
                    account_statement_list_params.AccountStatementListParams,
                ),
            ),
            model=AccountStatement,
        )


class AsyncAccountStatements(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccountStatementsWithRawResponse:
        return AsyncAccountStatementsWithRawResponse(self)

    async def retrieve(
        self,
        account_statement_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountStatement:
        """
        Retrieve an Account Statement

        Args:
          account_statement_id: The identifier of the Account Statement to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/account_statements/{account_statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountStatement,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        statement_period_start: account_statement_list_params.StatementPeriodStart | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[AccountStatement, AsyncPage[AccountStatement]]:
        """
        List Account Statements

        Args:
          account_id: Filter Account Statements to those belonging to the specified Account.

          cursor: Return the page of entries after this one.

          limit: Limit the size of the list that is returned. The default (and maximum) is 100
              objects.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/account_statements",
            page=AsyncPage[AccountStatement],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "cursor": cursor,
                        "limit": limit,
                        "statement_period_start": statement_period_start,
                    },
                    account_statement_list_params.AccountStatementListParams,
                ),
            ),
            model=AccountStatement,
        )


class AccountStatementsWithRawResponse:
    def __init__(self, account_statements: AccountStatements) -> None:
        self.retrieve = to_raw_response_wrapper(
            account_statements.retrieve,
        )
        self.list = to_raw_response_wrapper(
            account_statements.list,
        )


class AsyncAccountStatementsWithRawResponse:
    def __init__(self, account_statements: AsyncAccountStatements) -> None:
        self.retrieve = async_to_raw_response_wrapper(
            account_statements.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            account_statements.list,
        )
