import React, { Component } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';
import styled from 'styled-components';
import Head from 'next/head';
import Error from './ErrorMessage';

class Comment extends Component {
	render() {
		const { comment } = this.props;
		console.log(comment);
		return (
			<div>
				<p>
					<span>{comment.content}</span>
					<span>{comment.author.name}</span>
				</p>
			</div>
		);
	}
}

export default Comment;
export { BILL_COMMENT_QUERY };
