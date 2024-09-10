import React, { Component } from 'react';
import Downshift, { resetIdCounter } from 'downshift';
import Router from 'next/router';
import { ApolloConsumer } from 'react-apollo';
import gql from 'graphql-tag';
import debounce from 'lodash.debounce';
import { DropDown, DropDownItem, SearchStyles } from '../styles/DropDown';

const SEARCH_POLITICIANS_QUERY = gql`
	query SEARCH_POLITICIANS_QUERY($searchTerm: String!) {
		politicians(where: { OR: [{ name_contains: $searchTerm }, { state_contains: $searchTerm }] }) {
			id
			image
			name
		}
	}
`;

function routeToItem(politician) {
	Router.push({
		pathname: '/politician',
		query: {
			id: politician.id
		}
	});
}

// TODO: use enums and state to create prop for using search
// to make other queries

class AutoComplete extends Component {
	state = {
		politicians: [],
		loading: false
	};
	onChange = debounce(async (e, client) => {
		console.log('Searching...');
		// turn loading on
		this.setState({ loading: true });
		// Manually query apollo client
		const res = await client.query({
			query: SEARCH_POLITICIANS_QUERY,
			variables: { searchTerm: e.target.value }
		});
		this.setState({
			politicians: res.data.politicians,
			loading: false
		});
	}, 350);
	render() {
		resetIdCounter();
		return (
			<SearchStyles>
				<Downshift
					onChange={routeToItem}
					itemToString={(politician) =>

							politician === null ? '' :
							politician.name}
				>
					{({ getInputProps, getItemProps, isOpen, inputValue, highlightedIndex }) => (
						<div>
							<ApolloConsumer>
								{(client) => (
									<input
										{...getInputProps({
											type: 'search',
											placeholder: 'Search By Name or State',
											id: 'search',
											className:
												this.state.loading ? 'loading' :
												'',
											onChange: (e) => {
												e.persist();
												this.onChange(e, client);
											}
										})}
									/>
								)}
							</ApolloConsumer>
							{isOpen && (
								<DropDown>
									{this.state.politicians.map((politician, index) => (
										<DropDownItem
											{...getItemProps({
												politician
											})}
											key={politician.id}
											highlighted={index === highlightedIndex}
										>
											<img width="50" src={politician.image} alt={politician.name} />
											{politician.name}
										</DropDownItem>
									))}
									{!this.state.politicians.length &&
									!this.state.loading && <DropDownItem>Nothing Found {inputValue}</DropDownItem>}
								</DropDown>
							)}
						</div>
					)}
				</Downshift>
			</SearchStyles>
		);
	}
}

export default AutoComplete;
