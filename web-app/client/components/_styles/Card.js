import styled from 'styled-components';

const Card = styled.div`
	* {
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
		@import url('https://fonts.googleapis.com/css?family=Inconsolata'),
			font-size: 1rem;
		font-family: 'Inconsolata', monospace;
	}

	img {
		height: 250px;
		width: 100%;
		object-fit: cover;
		object-position: 0 0;
	}

	body {
		background-color: #ecf0f1;
	}

	header {
		display: block;
		overflow: hidden;
		position: relative;
		padding-bottom: 2em;
		-moz-border-radius-topleft: 8px;
		-webkit-border-top-left-radius: 8px;
		border-top-left-radius: 8px;
		-moz-border-radius-topright: 8px;
		-webkit-border-top-right-radius: 8px;
		border-top-right-radius: 8px;
	}

	.container {
		width: 260px;
		margin: 3em auto 1em auto;
		-webkit-border-radius: 8px;
		-moz-border-radius: 8px;
		-ms-border-radius: 8px;
		-o-border-radius: 8px;
		border-radius: 8px;
		padding-bottom: 1.5em;
		background-color: ${(props) => props.theme.grey2};
		-webkit-box-shadow: #bdc3c7 0 5px 5px;
		-moz-box-shadow: #bdc3c7 0 5px 5px;
		box-shadow: #bdc3c7 0 5px 5px;
	}

	.bg {
		border-bottom: 8px solid ${(props) => props.theme.secondary};
	}

	.bio:hover > .desc {
		cursor: pointer;
		opacity: 1;
	}

	.avatarcontainer {
		position: absolute;
		bottom: 0;
		right: 0;
		left: 0;
		margin: auto;
		width: 70px;
		height: 70px;
		display: block;
	}
	.avatarcontainer:hover > .hover {
		opacity: 1;
	}

	.avatar {
		width: 100%;
		border: 8px solid #5cc0ff;
		-webkit-border-radius: 50%;
		-moz-border-radius: 50%;
		-ms-border-radius: 50%;
		-o-border-radius: 50%;
		border-radius: 50%;
		overflow: hidden;
		position: relative;
	}
	.avatar img {
		width: 65px;
		height: 65px;
	}
	.avatar:hover + .hover {
		opacity: 1;
		cursor: pointer;
	}

	.hover {
		position: absolute;
		cursor: pointer;
		width: 100%;
		height: 100%;
		background-color: #3498db;
		top: 0;
		font-size: 1.8em;
		text-align: center;
		color: white;
		padding-top: 18%;
		opacity: 0;
		font-family: 'FontAwesome';
		font-weight: 300;
		border: 8px solid #5cc0ff;
		-webkit-border-radius: 50%;
		-moz-border-radius: 50%;
		-ms-border-radius: 50%;
		-o-border-radius: 50%;
		border-radius: 50%;
		-webkit-transition-property: all;
		-moz-transition-property: all;
		-o-transition-property: all;
		transition-property: all;
		-webkit-transition-duration: 0.5s;
		-moz-transition-duration: 0.5s;
		-o-transition-duration: 0.5s;
		transition-duration: 0.5s;
		-webkit-transition-timing-function: ease;
		-moz-transition-timing-function: ease;
		-o-transition-timing-function: ease;
		transition-timing-function: ease;
	}

	.data {
		margin-top: .6em;
		color: #81878b;
	}
	.data li {
		width: 32%;
		text-align: center;
		display: inline-block;
		font-size: 1.5em;
		font-family: 'Lato';
		border-right: solid 1px #bdc3c7;
	}
	.data li:last-child {
		border: none;
	}
	.data li span {
		display: block;
		/*text-transform: uppercase;*/
		font-family: 'Quicksand';
		font-size: .5em;
		margin-top: .6em;
		font-weight: 700;
	}

	.desc {
		position: absolute;
		top: 0;
		background-color: rgba(0, 0, 0, 0.6);
		width: 100%;
		height: 171px;
		padding: 1.2em 1em 0 1em;
		color: white;
		text-align: center;
		opacity: 0;
		-webkit-transition-property: all;
		-moz-transition-property: all;
		-o-transition-property: all;
		transition-property: all;
		-webkit-transition-duration: 0.3s;
		-moz-transition-duration: 0.3s;
		-o-transition-duration: 0.3s;
		transition-duration: 0.3s;
		-webkit-transition-timing-function: ease-in;
		-moz-transition-timing-function: ease-in;
		-o-transition-timing-function: ease-in;
		transition-timing-function: ease-in;
	}
	.desc h3 {
		font-family: "Lato";
		font-size: 1.2em;
		margin-bottom: .5em;
	}
	.desc p {
		font-size: .9em;
		font-family: 'Quicksand';
		line-height: 1.5em;
	}

	.follow {
		margin: 1.5em auto 0 auto;
		background-color: ${(props) => props.theme.secondary} /*#2589cc;*/
		width: 150px;
		color: white;
		font-family: "Lato";
		text-align: center;
		padding: .5em;
		-webkit-border-radius: 5px;
		-moz-border-radius: 5px;
		-ms-border-radius: 5px;
		-o-border-radius: 5px;
		border-radius: 5px;
		-webkit-transition-property: all;
		-moz-transition-property: all;
		-o-transition-property: all;
		transition-property: all;
		-webkit-transition-duration: 0.3s;
		-moz-transition-duration: 0.3s;
		-o-transition-duration: 0.3s;
		transition-duration: 0.3s;
		-webkit-transition-timing-function: ease;
		-moz-transition-timing-function: ease;
		-o-transition-timing-function: ease;
		transition-timing-function: ease;
	}
	.follow:hover {
		background-color: #167abd;
		cursor: pointer;
	}
`;

export default Card;
const old = styled.div`
	a {
		font-size: 2rem;
		text-align: center;
	}
	img {
		width: 100%;
		height: 20px;
		object-fit: cover;
	}
	infoList {
		font-size: 1.75rem;
		line-height: 0;
		font-weight: 300;
		flex-grow: 0;
		padding: 0 1rem;
		font-size: 1.5rem;
		text-align: left;
	}
	buttonList {
		position: relative;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: center;
		width: 100%;
		border-top: 1px solid ${(props) => props.theme.lightgrey};
		border-right: 1px solid ${(props) => props.theme.lightgrey};

		background: ${(props) => props.theme.white};
		& > * {
			background: white;
			border: 0;
			font-size: 2rem;
			padding: 0rem;
			position: center;
		}
	}
`;

const Name = styled.p`
	margin: 0 1rem;
	text-align: center;
	transform: skew(0deg) rotate(0deg);
	margin-top: -3rem;
	text-shadow: 2px 2px 0 rgba(0, 0, 0, 0.1);
	a {
		background: ;
		display: inline;
		line-height: 10;
		font-size: 1rem;
		text-align: center;
		color: ${(props) => props.theme.black};
		padding: 0 1rem;
	}
	p {
		text-align: left;
	}
`;
