import React, { Component } from 'react';
import { Query } from 'react-apollo';
import gql from 'graphql-tag';
import styled from 'styled-components';
import PoliticianCard from './PoliticianCard';
import Pagination from '../Main/Pagination';
import { perPage } from '../../../spotlight-app/frontend/config';

const ALL_POLITICIANS_QUERY = gql`
	query ALL_POLITICIANS_QUERY($skip: Int = 0, $first: Int = ${perPage}) {
		politicians(first: $first, skip: $skip, orderBy: createdAt_DESC) {
			id
			party
			name
			title
			chamber
			state
			district
			nthCongress
			phone
			gender
			image
			largeImage
			website
			govUrl
			createdAt
			updatedAt



		}
	}
`;

const Center = styled.div`text-align: center;`;
const PoliticiansList = styled.div`
	display: grid;
	grid-template-columns: 1fr 1fr;
	grid-gap: 60px;
	max-width: ${(props) => props.theme.maxWidth};
	margin: 0 auto;
`;

class Politicians extends Component {
	render() {
		return (
			<Center>
				<Pagination page={this.props.page} />
				<Query
					query={ALL_POLITICIANS_QUERY}
					variables={{
						skip: this.props.page * perPage - perPage
					}}
				>
					{({ data, error, loading }) => {
						if (loading) return <p>Loading...</p>;
						if (error) return <p>Error: {error.message}</p>;
						return (
							<PoliticiansList>
								{data.politicians.map((politician) => (
									<PoliticianCard politician={politician} key={politician.id} />
								))}
							</PoliticiansList>
						);
					}}
				</Query>
				<Pagination page={this.props.page} />
			</Center>
		);
	}
}

export default Politicians;
export { ALL_POLITICIANS_QUERY };
