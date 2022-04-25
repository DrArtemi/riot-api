<script>
    import Search from '../components/search/Search.svelte'
    import League from '../components/League.svelte';
    import { page } from '$app/stores'

    const category = $page.query.get('category');
    const slug = $page.query.get('slug');
</script>

<div class="search-bar">
    <Search />
</div>

<div class="content">
{#if category == "leagues" && slug}
    <League slug={slug}/>
{/if}
</div>

<style>
    .search-bar {
        margin-left: auto;
        margin-right: auto;
        margin-top: 2rem;
        width: 80%;
        padding: .5rem 2rem;
        border-radius: 5px;
        box-shadow: 0rem 0rem .25rem #b0bec5;
    }

    .content {
        margin-left: auto;
        margin-right: auto;
        margin-top: 2rem;
        width: 80%;
        padding: .5rem 2rem;
        border-radius: 5px;
        box-shadow: 0rem 0rem .25rem #b0bec5;
    }
</style>