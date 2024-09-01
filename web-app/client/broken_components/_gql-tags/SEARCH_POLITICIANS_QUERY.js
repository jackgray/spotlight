// import gql from 'graphql-tag';

// export default (SEARCH_POLITICIANS_QUERY = gql`
// 	query SEARCH_POLITICIANS_QUERY($searchTerm: String!) {
// 		politician(
// 			where: {
// 				OR: [
// 					{ name_contains: $searchTerm }
// 					{ description_contains: $searchTerm }
// 				]
// 			}
// 		) {
// 			id
// 			image
// 			name
// 		}
// 	}
// `);
