import Politicians from '../components/Politician/Politicians';

const Home = (props) => (
	<div>
		<Politicians page={parseFloat(props.query.page) || 1} />
	</div>
);

export default Home;
