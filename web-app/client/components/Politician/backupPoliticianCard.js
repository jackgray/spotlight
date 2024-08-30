import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Link from 'next/link';
import Name from './styles/Name';
import PoliticianStyles from './styles/PoliticianStyles';
import DeletePolitician from './DeletePolitician';
import FollowPolitician from './FollowPolitician';
import UnfollowPolitician from './UnfollowPolitician';
// Styles
import Card from './styles/Card';

class PoliticianCard extends Component {
	render() {
		const { politician } = this.props;
		return (
			<Card>
				<Link
					href={{
						pathname: '/politician',
						query: { id: politician.id }
					}}
				>
					<a href="">
						{politician.image && (
							<img src={politician.image} alt={politician.name} />
						)}
					</a>
				</Link>
				<div className="Name">
					<Link
						href={{
							pathname: '/politician',
							query: { id: politician.id }
						}}
					>
						<a href="">{politician.name}</a>
					</Link>
				</div>
				<div className="infoList">
					<p>{politician.party}</p>
					<p>{politician.chamber}</p>
					<p>{politician.district}th District</p>
					<p>{politician.state}</p>
					<a href={politician.website}>{politician.website}</a>
				</div>
				<div className="buttonList">
					<Link
						href={{
							pathname: '/update',
							query: { id: politician.id }
						}}
					>
						<p>✏️</p>
					</Link>
					<FollowPolitician id={politician.id}>❤️</FollowPolitician>
					<UnfollowPolitician id={politician.id}>
						💔
					</UnfollowPolitician>
					<DeletePolitician id={politician.id}>✖️</DeletePolitician>
				</div>
			</Card>
		);
	}
}

export default PoliticianCard;

/*


    render() {
		const { politician } = this.props;
		return (
			<PoliticianStyles>
				{politician.image && <img src={politician.image} alt={politician.name} />}
				<Name>
					<Link
						href={{
							pathname: '/politician',
							query: { id: politician.id }
						}}
					>
						<a href="">{politician.name}</a>
					</Link>
				</Name>
				<p>{politician.age}</p>
				<div className="buttonList">
					<Link
						href={{
							pathname: '/update',
							query: { id: politician.id }
						}}
					>
						<a>✏️</a>
					</Link>
					<button>❤️</button>
				</div>
			</PoliticianStyles>
		);
	}*/

/*
	render() {
		const { politician } = this.props;
		return (
			<Row>
				<Col sm="6">
					<Card body>
						<CardTitle>
							<Name>
								<Link
									href={{
										pathname: '/politician',
										query: {
											id: politician.id
										}
									}}
								>
									<a>{politician.name}</a>
								</Link>
							</Name>
						</CardTitle>
						<CardText>{politician.age}</CardText>
						<Button>❤️</Button>
					</Card>
				</Col>
			</Row>
		);
	}
}
*/
