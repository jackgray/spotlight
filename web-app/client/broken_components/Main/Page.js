import React, { Component } from 'react';
import Header from './Header';
import Meta from './Meta';
import styled, { ThemeProvider, injectGlobal } from 'styled-components';

const theme = {
	primary: '#f44242', // soft red
	secondary: '#2589cc', // twitter blue
	backgroundWhite: '#fcfcfc',
	red: '#38a8ff',
	black: '#393939',
	darkGrey: '#3A3A3A',
	grey2: '#dde1e2',
	lightGrey: '#E1E1E1',
	lightblue: '#54dfff',
	torquiose: '#3dfff2',
	lightRed: '#ff4635',
	offWhite: '#fcfcfc',
	cream: '#fffdf2',
	maxWidth: '1000px',
	bs: '0 12px 24px 0 rgba(0, 0, 0, 0.09)'
};

const StyledPage = styled.div`
	background: ${(props) => props.theme.offWhite};
	color: black;
`;

const Inner = styled.div`
	max-width: 1000px;
	margin: 0 auto;
	padding: 2rem;
	background: ${(props) => props.theme.offWhite};
`;

injectGlobal`
	@import url('https://fonts.googleapis.com/css?family=Inconsolata');
	@import url('https://fonts.googleapis.com/css?family=Major+Mono+Display');

	@font-face {
		font-family: 'Inconsolata';

	}
	html {
		box-sizing: border-box;
		font-size: 8px;
	}
	*, *:before, *:after {
		box-sizing: inherit;
	}
	body {
		padding: 0;
		margin: 0;
		font-size: 1.75rem;
		line-height: 2;
		font-family: 'Inconsolata';
	}
	a {
		text-decoration: none;
		color: ${theme.black}
		font-size: 2rem;
	}
	button {


		border: none;
	}
`;

// for injectGlobal, if theme def were not in this file
// it would have to be refactored into its own file and
// imported back in to have access to its props

class Page extends Component {
	render() {
		return (
			<ThemeProvider theme={theme}>
				<StyledPage>
					<Meta />
					<Header />
					<Inner>{this.props.children}</Inner>
				</StyledPage>
			</ThemeProvider>
		);
	}
}

export default Page;
