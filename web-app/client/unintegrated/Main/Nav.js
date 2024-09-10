import Link from 'next/link';
import NavStyles from '../styles/NavStyles';

const Nav = () => {
	return (
		<NavStyles>
			<Link href="/feed">
				<a>Feed</a>
			</Link>
			<Link href="/myImpact">
				<a>Engage!</a>
			</Link>
			<Link href="/people">
				<a>People</a>
			</Link>

			<Link href="/bills">
				<a>Bills</a>
			</Link>

			<Link href="/mypoliticians">
				<a>My Politicians</a>
			</Link>

			<Link href="/mybills">
				<a>My Bills</a>
			</Link>
			<Link href="/congresstoday">
				<a>Congress Today</a>
			</Link>
			<Link href="/about">
				<a>About</a>
			</Link>

			<Link href="/comingsoon">
				<a>Upcoming Features</a>
			</Link>
			<Link href="/login">
				<a>Log In</a>
			</Link>

			<Link href="/signup">
				<a>Sign Up</a>
			</Link>
			<Link href="/add">
				<a>Add To Database</a>
			</Link>
		</NavStyles>
	);
};

export default Nav;
