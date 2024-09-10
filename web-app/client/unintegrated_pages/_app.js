import App, { Container } from 'next/app';
import { ApolloProvider } from 'react-apollo';
import withData from '../lib/withData';
import Page from '../components/Main/Page';

class MyApp extends App {
	// getInitialProps is a special next.js lifecycle method
	// it will run before the initial page render and make
	// props available
	// it will do this for every page that loads
	// more info in video 15
	static async getInitialProps({ Component, ctx }) {
		let pageProps = {};
		if (Component.getInitialProps) {
			pageProps = await Component.getInitialProps(ctx);
		}
		// exposes query to the user
		pageProps.query = ctx.query;
		return { pageProps };
	}
	render() {
		const { Component, apollo, pageProps } = this.props;

		return (
			<Container>
				<ApolloProvider client={apollo}>
					<Page>
						<Component {...pageProps} />
					</Page>
				</ApolloProvider>
			</Container>
		);
	}
}

export default withData(MyApp);
