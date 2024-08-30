import React, { Component } from 'react';
import Router from 'next/router';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Form from '../styles/Form';
import Error from '../ErrorMessage';
import { ALL_BILLS_QUERY } from '../_gql-tags/ALL_BILLS_QUERY';

// TODO: connect bills to their sponsor
// (sponsor connection input type is BillCreateInput)

const CREATE_BILL_MUTATION = gql`
	mutation CREATE_BILL_MUTATION(
		$code: String
		$title: String!
		$summary: String
		$committees: String
		$sponsor: String
	) {
		createBill(code: $code, title: $title, summary: $summary, committees: $committees, sponsor: $sponsor) {
			id
		}
	}
`;

class CreateBill extends Component {
	state = {
		code: '',
		title: '',
		summary: '',
		committees: '',
		sponsor: ''
	};
	handleChange = (e) => {
		const { name, type, value } = e.target;

		const val =

				type === 'number' ? parseFloat(value) :
				value;
		this.setState({ [name]: val });
	};

	// refresh the query and update the cache

	render() {
		return (
			<Mutation mutation={CREATE_BILL_MUTATION} variables={this.state}>
				{(createBill, { loading, error }) => (
					<Form
						onSubmit={async (e) => {
							e.preventDefault();
							const res = await createBill();
							console.log(res);
							Router.push({
								pathname: '/bills',
								query: { id: res.data.createBill.id }
							});
						}}
					>
						<Error error={error} />
						<fieldset disabled={loading} aria-busy={loading}>
							<label htmlFor="code">
								Bill Number
								<input
									type="text"
									id="code"
									name="code"
									placeholder="Bill Number"
									value={this.state.code}
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
									value={this.state.title}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="summary">
								Summary
								<input
									type="text"
									id="summary"
									name="summary"
									placeholder="State"
									value={this.state.summary}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="committees">
								Committees
								<input
									type="text"
									id="committees"
									name="committees"
									placeholder="Committees"
									value={this.state.committees}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="committees">
								Sponsor
								<input
									type="text"
									id="sponsor"
									name="sponsor"
									placeholder="Sponsored By"
									value={this.state.sponsor}
									onChange={this.handleChange}
								/>
							</label>
							<button type="submit">Submit</button>
						</fieldset>
					</Form>
				)}
			</Mutation>
		);
	}
}

export default CreateBill;
export { CREATE_BILL_MUTATION };
