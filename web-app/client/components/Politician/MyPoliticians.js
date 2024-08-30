import React, { Component } from 'react';
import { Query } from 'react-apollo';
import gql from 'graphql-tag';
import styled from 'styled-components';
import { perPage } from '../../../spotlight-app/frontend/config';
import PoliticianCard from './PoliticianCard';

const MY_POLITICIANS_QUERY = gql`
	query MY_POLITICIANS_QUERY {
		me {
			myPoliticians {
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

class MyPoliticians extends Component {
	render() {
		return (
			<Center>
				<Query
					query={MY_POLITICIANS_QUERY}
					variables={
						({
							skip: this.props.page * perPage - perPage
						},
						{ id: this.props.id })
					}
				>
					{({ data, error, loading }) => {
						if (loading) return <p>Loading...</p>;
						if (error) return <p>Error: {error.message}</p>;
						const myPoliticians = data.me.myPoliticians;
						console.log('loading myPolitician politicians...');
						console.log(myPoliticians.id);
						return (
							<PoliticiansList>
								{myPoliticians.map((politician) => (
									<PoliticianCard politician={politician} key={politician.id} />
								))}
							</PoliticiansList>
						);
					}}
				</Query>
			</Center>
		);
	}
}

export default MyPoliticians;
export { MY_POLITICIANS_QUERY };
