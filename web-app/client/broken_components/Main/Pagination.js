// Wrapper component to separate query results into pages
// defined by perPage in config.js

// dependencies
import React from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';
import Head from 'next/head';
import Link from 'next/link';
// config files. perPage = number of elements to show on each page
import { perPage } from '../../config';
// styled components
import PaginationStyles from '../styles/PaginationStyles';

const PAGINATION_QUERY = gql`
	query PAGINATION_QUERY {
		politiciansConnection {
			aggregate {
				count
			}
		}
	}
`;

const Pagination = (props) => (
	<Query query={PAGINATION_QUERY}>
		{({ data, loading, error }) => {
			if (loading) return <p>Loading...</p>;
			const count = data.politiciansConnection.aggregate.count;
			const pages = Math.ceil(count / perPage);
			const page = parseInt(props.page, 10); // force pageProps as integer

			return (
				<PaginationStyles>
					<Head>
						<title>
							GovTrackr | Page {page} of {pages}
						</title>
					</Head>
					<Link
						prefetch
						href={{
							pathname: 'people',
							query: { page: page - 1 }
						}}
					>
						<a className="prev" aria-disabled={page <= 1}>
							Prev
						</a>
					</Link>
					<p>
						{props.page} of{' '}
						<span className="totalPages">{pages}</span> pages
					</p>
					<p> {count} Total</p>
					<Link
						prefetch
						href={{
							pathname: 'people',
							query: { page: page + 1 }
						}}
					>
						<a className="next" aria-disabled={page >= pages}>
							Next
						</a>
					</Link>
				</PaginationStyles>
			);
		}}
	</Query>
);

export default Pagination;
export { PAGINATION_QUERY };
