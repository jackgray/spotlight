const About = (props) => (
	<div>
		<p>There is no arrangement of facts that is unbiased.</p>
		<p>Arrange your own facts.</p>
		<p>{props.children}</p>
	</div>
);

export default About;
