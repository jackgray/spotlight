import UpdatePolitician from '../components/Politician/UpdatePolitician';

const Update = ({ query }) => (
	<div>
		<UpdatePolitician id={query.id} />
	</div>
);

export default Update;
