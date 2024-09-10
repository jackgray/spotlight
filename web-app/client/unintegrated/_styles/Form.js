import styled, { keyframes } from 'styled-components';

const loading = keyframes`
  from {
    background-position: 0 0;
    /* rotate: 0; */
  }

  to {
    background-position: 100% 100%;
    /* rotate: 360deg; */
  }
`;

const Form = styled.form`
	box-shadow: 0 0 5px 3px rgba(0, 0, 0, 0.05);
	background: rgba(0, 0, 0, 0.02);
	border: 5px solid white;
	padding: 20px;
	font-size: 1.5rem;
	line-height: 1.5;
	font-weight: 600;
	label {
		display: block;
		margin-bottom: 1rem;
		margin-right: 1rem;
		padding-right: 50px;
	}
	input,: 0.5rem;
	textarea,
	select {
		width: 100%;
		padding: 1rem;
		border: 1px solid black;
		&:focus {
			outline: 0;
			border-color: ${(props) => props.theme.lightRed};
		}
	}
	button,
	input[type='submit'] {
		width: auto;
		background: ${(props) => props.theme.lightRed};
		color: white;
		border: 0;
		font-size: 2rem;
		font-weight: 600;
		padding: .5rem 1.2rem;
	}
	fieldset {
		border: 0;
		padding: 0;

		&[disabled] {
			opacity: 0.5;
		}
		&::before {
			height: 10px;
			margin-bottom: 10px;
			content: '';
		}
		&[aria-busy='true']::before {
			background-size: 50% auto;
			animation: ${loading} 0.5s linear infinite;
		}
	}
	,
	/* The switch - the box around the slider */ .switch {
		position: relative;
		display: inline-block;
		width: 60px;
		height: 34px;
	}

	/* Hide default HTML checkbox */
	.switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	input:checked + .slider {
		background-color: #2196f3;
	}

	input:focus + .slider {
		box-shadow: 0 0 1px #2196f3;
	}

	input:checked + .slider:before {
		-webkit-transform: translateX(26px);
		-ms-transform: translateX(26px);
		transform: translateX(26px);
	}

	/* Rounded sliders */
	.slider.round {
		border-radius: 34px;
	}

	.slider.round:before {
		border-radius: 50%;
	}
`;

Form.displayName = 'Form';

export default Form;
