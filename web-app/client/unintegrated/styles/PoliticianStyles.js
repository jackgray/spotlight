import styled from 'styled-components';

const PoliticianStyles = styled.div`
	background: white;
	border: 1px solid ${(props) => props.theme.offWhite};
	box-shadow: ${(props) => props.theme.bs};
	position: relative;
	display: flex;
	flex-direction: column;
	max-height: 350px;
	a {
		font-size: 2rem;
		text-align: center;
	}
	img {
		width: 100%;
		height: 200px;
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

export default PoliticianStyles;
