import React, { Component } from 'react';
import { Query } from 'react-apollo';
import gql from 'graphql-tag';
import styled from 'styled-components';
import { perPage } from '../../config';
import Bill from './Bill';

const MY_BILLS_QUERY = gql`
	query MY_BILLS_QUERY {
		me {
			myBills {
				id
				code
				title
				upvotes {
					name
				}
				downvotes {
					name
				}
				followers {
					name
				}
			}
		}
	}
`;

const Center = styled.div`text-align: center;`;
const BillsList = styled.div`
	display: grid;
	grid-template-columns: 1fr 1fr;
	grid-gap: 60px;
	max-width: ${(props) => props.theme.maxWidth};
	margin: 0 auto;
`;

class MyBills extends Component {
	render() {
		return (
			<Center>
				<Query
					query={MY_BILLS_QUERY}
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
						const myBills = data.me.myBills;
						console.log('loading myBill bills...');
						console.log(myBills.id);
						return <BillsList>{myBills.map((bill) => <Bill bill={bill} key={bill.id} />)}</BillsList>;
					}}
				</Query>
			</Center>
		);
	}
}

export default MyBills;
export { MY_BILLS_QUERY };
