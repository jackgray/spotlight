import Link from 'next/link';
import Politicians from '../components/Politician/Politicians';

const PoliticiansPage = (props) => (
	<div>
		<Politicians page={props.query.page || 1} />
	</div>
);

export default PoliticiansPage;
