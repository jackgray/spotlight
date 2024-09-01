import React, { Component } from 'react';
import Router from 'next/router';
import { Mutation, Query } from 'react-apollo';
import gql from 'graphql-tag';
import Form from '../styles/Form';
import Error from '../ErrorMessage';

const SINGLE_BILL_QUERY = gql`
	query SINGLE_BILL_QUERY($id: ID!) {
		bill(where: { id: $id }) {
			id
			code
			title
		}
	}
`;

const UPDATE_BILL_MUTATION = gql`
	mutation UPDATE_BILL_MUTATION($id: ID, $code: String, $title: String) {
		updateBill(id: $id, code: $code, title: $title) {
			id
			code
			title
		}
	}
`;

class UpdateBill extends Component {
	state = {};
	handleChange = (e) => {
		const { name, type, value } = e.target;

		const val =

				type === 'number' ? parseFloat(value) :
				value;
		this.setState({ [name]: val });
	};

	updateBill = async (e, updateBillMutation) => {
		e.preventDefault();
		console.log('Updating Bill');
		console.log(this.state);
		const res = await updateBillMutation({
			variables: {
				id: this.props.id,
				...this.state
			}
		});
		console.log('Updated!');
	};

	render() {
		return (
			<Query query={SINGLE_BILL_QUERY} variables={{ id: this.props.id }}>
				{({ data, loading }) => {
					if (loading) return <p>Loading...</p>;
					if (!data.bill) return <p>No bill found in database for {this.props.id}</p>;
					return (
						<Mutation mutation={UPDATE_BILL_MUTATION} variables={this.state}>
							{(updateBill, { loading, error }) => (
								<Form onSubmit={(e) => this.updateBill(e, updateBill)}>
									<Error error={error} />
									<fieldset disabled={loading} aria-busy={loading}>
										<label htmlFor="code">
											Code
											<input
												type="text"
												id="code"
												name="code"
												placeholder="Code"
												defaultValue={data.bill.code}
												onChange={this.handleChange}
											/>
										</label>

										<label htmlFor="title">
											Title
											<input
												type="text"
												id="title"
												name="title"
												placeholder="Title"
												defaultValue={data.bill.title}
												onChange={this.handleChange}
											/>
										</label>

										<button type="submit">Save Changes</button>
									</fieldset>
								</Form>
							)}
						</Mutation>
					);
				}}
			</Query>
		);
	}
}

export default UpdateBill;
export { UPDATE_BILL_MUTATION };
