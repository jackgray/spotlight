import React, { Component } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';
import styled from 'styled-components';
import Head from 'next/head';
import Error from '../ErrorMessage';
import UpvoteBill from './UpvoteBill';
import DownvoteBill from './DownvoteBill';
import CreateComment from '../CreateComment';
import Comments from '../Comments';
import Comment from '../Comment';
import SingleBillStyles from '../styles/SingleBillStyles';

import CURRENT_USER_QUERY from '../User/User';
import SINGLE_BILL_QUERY from '../_gql-tags/SINGLE_BILL_QUERY';

class SingleBill extends Component {
	_updateCacheAfterComment = (cache, commentBill, billId) => {
		const data = cache.readQuery({ query: SINGLE_BILL_QUERY });
		const commentedBill = data.bills.find((bill) => bill.id === billId);
		commentedBill.comments = createComment.bill.comments;
		cache.writeQuery({ query: SINGLE_BILL_QUERY, data });
	};

	render() {
		return (
			<Query query={SINGLE_BILL_QUERY} variables={{ id: this.props.id }}>
				{({ error, loading, data }) => {
					if (error) return <Error error={error} />;
					if (loading) return <p>Loading...</p>;
					if (!data.bill) return <p>no data for id: {this.props.id}</p>;

					const bill = data.bill;
					const comments = data.comment;
					console.log('comments:', comments);
					console.log('author:', bill.comments.author);
					const score = bill.upvotes.length - bill.downvotes.length;

					return (
						<SingleBillStyles>
							<Head>
								<title>GovTrackr | {bill.name}</title>
							</Head>

							<div>
								<h2 className="details">Code: {bill.code}</h2>
								<p>ID: {bill.id}</p>
								<p>Title: {bill.title}</p>
								<p>Summary: {bill.summary}</p>
								<p>Chamber of Congress: {bill.chamber}</p>
								<p>{bill.committees}</p>
								<div>
									<span>
										<UpvoteBill id={bill.id}>👍</UpvoteBill>
									</span>
									<span>{score}</span>
									<DownvoteBill>👎</DownvoteBill>
								</div>
								<div>
									<Comments
										bill={data.bill}
										key={data.bill.id}
										updateStoreAfterComment={this._updateCacheAfterComment}
									/>
								</div>
							</div>
						</SingleBillStyles>
					);
				}}
			</Query>
		);
	}
}

export default SingleBill;
export { SINGLE_BILL_QUERY };
