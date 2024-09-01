import Link from 'next/link';
import BillList from '../components/Bill/BillList';

const BillsPage = (props) => (
	<div>
		<BillList page={props.query.page || 1} />
	</div>
);

export default BillsPage;
