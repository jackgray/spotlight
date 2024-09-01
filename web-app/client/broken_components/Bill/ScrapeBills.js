import React, { Component } from 'react';
import Router from 'next/router';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Form from '../styles/Form';
import Error from '../ErrorMessage';
import { ALL_BILLS_QUERY } from './Bills';

const SCRAPE_BILLS_MUTATION = gql`
	mutation SCRAPE_BILLS_MUTATION($number: Int, $title: String!, $summary: String, $committees: String) {
		scrapeBills(number: $number, title: $title, summary: $summary, committees: $committees) {
			id
		}
	}
`;

class ScrapeBills extends Component {
	state = {
		number: 0,
		title: '',
		summary: '',
		committees: ''
	};
	handleChange = (e) => {
		const { name, type, value } = e.target;

		const val =

				type === 'number' ? parseFloat(value) :
				value;
		this.setState({ [name]: val });
	};

	render() {
		return (
			<Mutation mutation={SCRAPE_BILLS_MUTATION} variables={this.state}>
				{(scrapeBills, { loading, error }) => (
					<button
						onClick={async (e) => {
							e.preventDefault();
							const res = await scrapeBills();
							console.log(res);
							Router.push({
								pathname: '/',
								query: { id: res.data.scrapeBills.id }
							});
						}}
					>
						Scrape Bills
					</button>
				)}
			</Mutation>
		);
	}
}

export default ScrapeBills;
export { SCRAPE_BILLS_MUTATION };
