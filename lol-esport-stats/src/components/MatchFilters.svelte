<script>
	export let tournaments;
	export let tournaments_stages;
	export let tournaments_filters;
	export let stages_filters;

	// Handle filters checkboxes events
	function updateTournamentFilter(e) {
		if (!e.target.checked)
			stages_filters = stages_filters.filter(
				(el) => !tournaments_stages[e.target.value].includes(el)
			);
		else
			for (const stage_id of tournaments_stages[e.target.value])
				if (!stages_filters.includes(stage_id)) stages_filters.push(stage_id);
		stages_filters = [...stages_filters]; // C'est quand même fou de devoir faire ça fuck le js
	}

	function updateStageFilter(e) {
		if (e.target.checked) {
			for (const tournament in tournaments_stages)
				if (
					tournaments_stages[tournament].includes(e.target.value) &&
					!tournaments_filters.includes(tournament)
				)
					tournaments_filters.push(tournament);
			tournaments_filters = [...tournaments_filters]; // C'est quand même fou de devoir faire ça fuck le js
		}
	}
	// Display filters region
	let showFilters = false;
	function toggleFilters(e) {
		showFilters = !showFilters;
	}
</script>

<h2
	on:click={toggleFilters}
	class="text-slate-300 text-3xl w-full cursor-pointer hover:bg-slate-700 px-4 py-2"
>
	Filters
</h2>
{#if $tournaments.data}
	<div class="{showFilters ? '' : 'hidden'} max-h-56 px-4 pb-4 overflow-auto">
		{#each $tournaments.data.tournamentsBySlugs as tournament}
			<div class="mt-4">
				<label class="custom-box relative cursor-pointer capitalize text-slate-300 pl-6">
					{tournament.slug.replaceAll('_', ' ')}
					<input
						on:change={updateTournamentFilter}
						class="hidden"
						bind:group={tournaments_filters}
						type="checkbox"
						value={tournament.slug}
					/>
					<span class="checkmark absolute top-0 left-0 h-4 w-4 bg-slate-700 rounded-sm" />
				</label>
				{#if tournament.stages.length > 0}
					<div class="pl-6 mt-2">
						{#each tournament.stages as stage, i}
							<label
								class="custom-box relative cursor-pointer capitalize text-slate-300 pl-6 {i !== 0
									? 'ml-4'
									: ''}"
							>
								{stage.name}
								<input
									on:change={updateStageFilter}
									class="hidden"
									bind:group={stages_filters}
									type="checkbox"
									value={stage.id}
								/>
								<span class="checkmark absolute top-0 left-0 h-4 w-4 bg-slate-700 rounded-sm" />
							</label>
						{/each}
					</div>
				{/if}
			</div>
		{/each}
	</div>
{/if}

<style>
	.custom-box .checkmark:after {
		content: '';
		position: absolute;
		display: none;
	}

	.custom-box input:checked + .checkmark:after {
		display: block;
	}

	.custom-box .checkmark:after {
		left: 6px;
		top: 3px;
		width: 5px;
		height: 10px;
		border: solid white;
		border-width: 0 3px 3px 0;
		-webkit-transform: rotate(45deg);
		-ms-transform: rotate(45deg);
		transform: rotate(45deg);
	}
</style>
