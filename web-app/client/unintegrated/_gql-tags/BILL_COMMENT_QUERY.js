import gql from 'graphql-tag';

const BILL_COMMENT_QUERY = gql`
	query BILL_COMMENT_QUERY($id: ID!) {
		comment(where: { id: $id }) {
			id
			content
			author {
				name
			}
		}
	}
`;

export default BILL_COMMENT_QUERY;
