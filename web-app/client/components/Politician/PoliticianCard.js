import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Link from 'next/link';
import Name from '../styles/Name';
import PoliticianStyles from '../styles/PoliticianStyles';
import DeletePolitician from './DeletePolitician';
import FollowPolitician from './FollowPolitician';
import UnfollowPolitician from './UnfollowPolitician';
import UpdatePolitician from './UpdatePolitician';
// Styles
import Card from '../styles/Card';

class PoliticianCard extends Component {
	render() {
		const { politician } = this.props;
		return (
			<Card>
				<div className="container">
					<header>
						<div className="bio">
							<img src={politician.image} className="bg" />

							<div className="desc">
								<h3>{politician.name}</h3>
								<p>{politician.name}</p>
							</div>
						</div>
					</header>
					<div className="content">
						<div className="data">
							<h3>{politician.name}</h3>
							<ul>
								<li>
									<span>{politician.party}</span>
								</li>
								<li>
									<span>{politician.state}</span>
								</li>
								<li>
									<span>District: {politician.district}</span>
								</li>
							</ul>
						</div>
						<div className="follow">
							<FollowPolitician id={politician.id}>Follow</FollowPolitician>
						</div>
						<div className="follow">
							<Link
								href={{
									pathname: '/update',
									query: { id: politician.id }
								}}
							>
								<a>Edit</a>
							</Link>
						</div>
					</div>
				</div>
			</Card>
		);
	}
}

export default PoliticianCard;

/*
        <div class="content">
            <div class="data">
                <ul>
                    <li>
                        2,934
                        <span>Tweets</span>
                    </li>
                    <li>
                        1,119
                        <span>Followers</span>
                    </li>
                    <li>
                        530
                        <span>Following</span>
                    </li>
                </ul>
            </div>

            <div class="follow"> <div class="icon-twitter"></div> Follow</div>
        </div>

    </div>

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
