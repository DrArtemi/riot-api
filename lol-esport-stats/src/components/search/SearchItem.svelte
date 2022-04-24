<script>
    export let name;
    export let link;
</script>

<li class="search-item">
    <a href={link}>{name}</a>
</li>

<style>
    .search-item {
        list-style-type: none;
    }

    .search-item a {
        color: black;
        text-decoration: none;
        display: inline-block;
        padding: .4rem 1rem;
        width: 95%;
        border-radius: 5px;
    }

    .search-item a:hover {
        background-color: #eceff1;
    }
</style>