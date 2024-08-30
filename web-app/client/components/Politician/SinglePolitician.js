import React, { Component } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';
import styled from 'styled-components';
import Head from 'next/head';
import Error from '../ErrorMessage';

const SinglePoliticianStyles = styled.div`
	max-width: 600px;
	max-height: 100px;
	margin: 2rem auto;
	box-shadow: ${(props) => props.theme.bs}
	display: grid;
	grid-auto-columns: 1fr;
	grid-auto-flow: row;
	min-height: 800px;
	img {
		width:100%;
		height: 100%;
		max-height: 600px;
		object-fit: contain;
	}
	.details {
		margin: 3rem;
		font-size: 2rem;
	}
`;

const SINGLE_POLITICIAN_QUERY = gql`
	query SINGLE_POLITICIAN_QUERY($id: ID!) {
		politician(where: { id: $id }) {
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

class SinglePolitician extends Component {
	render() {
		return (
			<Query query={SINGLE_POLITICIAN_QUERY} variables={{ id: this.props.id }}>
				{({ error, loading, data }) => {
					if (error) return <Error error={error} />;
					if (loading) return <p>Loading...</p>;
					if (!data.politician) return <p>no data for id: {this.props.id}</p>;
					const politician = data.politician;
					return (
						<SinglePoliticianStyles>
							<Head>
								<title>GovTrackr | {politician.name}</title>
							</Head>
							<img src={politician.largeImage} alt={politician.name} />
							<div>
								<h2 className="details">{politician.name}</h2>
								<p>{politician.party}</p>
							</div>
						</SinglePoliticianStyles>
					);
				}}
			</Query>
		);
	}
}

export default SinglePolitician;
export { SINGLE_POLITICIAN_QUERY };
