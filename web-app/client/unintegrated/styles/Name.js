import styled from 'styled-components';

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

export default Name;
