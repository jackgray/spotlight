const ComingSoon = (props) => (
	<div>
		<p>Upcoming features:</p>
		<li>congress.gov data scraping</li>
		<li>people's votes on bills</li>
		<li>
			CongressToday component that shows live updates of congressional
			proceedings sorted by most popular, heighest/lowest approval, or
			chronologically. Show what's happening tomorrow.
		</li>
		<li>Archive access to video recordings on the floor</li>
		<li>SOON: comment on bills, elections, user created topics, etc.</li>
		<li>fix updateCache so that db changes update state</li>
		<p>Backend todos:</p>
		<li>
			switch from prisma-bindings to prisma-client and $fragments finish
			Notifications feature refresh cache on upvote/downvote create Topics
			page move all gql tags to centralized tags folder
		</li>
		<li>
			populate database of politicians and extant bills from public
			database if one exists
		</li>
	</div>
);

export default ComingSoon;
