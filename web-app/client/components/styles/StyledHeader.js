import styled from 'styled-components';

const StyledHeader = styled.header`
	.bar {
		border-bottom: 10px solid ${(props) => props.theme.primary};
		display: grid;
		grid-template-columns: auto 1fr;
		justiify-content: space-between;
		align-items: stretch;
		@media (max-width: 1300px) {
			grid-template-columns: 1fr;
			justify-content: center;
		}
	}
	.sub-bar {
		display: grid;
		grid-template-columns: 1fr auto;
		border-bottom: 1px solid ${(props) => props.theme.black};
	}
`;

export default StyledHeader;
