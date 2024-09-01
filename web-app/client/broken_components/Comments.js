import React, { Component } from 'react';
import Comment from './Comment';
import CreateComment from './CreateComment';

class Comments extends Component {
	render() {
		const { bill } = this.props;

		return (
			<div>
				<div>{bill.comments.map((comment) => <Comment comment={comment} key={comment.id} />)}</div>
				<div>
					<CreateComment bill={bill} key={bill.id} />
				</div>
			</div>
		);
	}
}

export default Comments;
