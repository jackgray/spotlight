import gql from 'graphql-tag';
import { perPage } from '../../../spotlight-app/frontend/config';

const BILL_LIST_QUERY = gql`
	query BILL_LIST_QUERY($skip: Int = 0, $first: Int = ${perPage}) {
		bills(first: $first, skip: $skip, orderBy: createdAt_DESC) {
			id
			code
			title
			summary
			committees
			upvotes {
				id
			}
			downvotes {
				id
			}
			followers {
				name
			}
		}
	}
`;

export default BILL_LIST_QUERY;
