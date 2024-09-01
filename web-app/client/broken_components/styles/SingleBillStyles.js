import styled from 'styled-components';

const SingleBillStyles = styled.div`
	max-width: 600px;
	max-height: 100px;
	margin: 10rem auto;
	box-shadow: ${(props) => props.theme.bs}
	display: grid;
	grid-auto-columns: 10fr;
	grid-auto-flow: row;
	min-height: 800px;
	img {
		width:100%;
		height: 100%;
		max-height: 600px;
		object-fit: contain;
	}
	.details {
		margin: 3rem;
		font-size: 2rem;
    }
    span {
        padding: 20px;
    }
`;

export default SingleBillStyles;
