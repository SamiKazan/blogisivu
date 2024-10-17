# blogisivu

tietokannat ja webohjelmointi course project <br />

<h1>Sovelluksen testaus: </h1>
(en saanut fly.io toimimaan)
1. start-pg.sh terminaalissa
2. toisessa terminaalissa avaa psql
3. kopioi schema.sql sisältö psql terminaaliin
4. avaa kolmas terminaali
5. mene projektin hakemistoon
6. source venv/bin/activate
7. flask run
8. avaa linkki


<h2>Esittely</h2>

<p>Blogisivu on sivusto, jossa käyttäjät voivat kirjoitaa, luonnostaa ja lähettää blogejaan muiden luettavaksi. Oleellinen osa sivustoa on mahdollisuus tykätä, kommentoida blogeja. Käyttäjät voivat hakea blogeja etsintäkentästä.</p>

<h2>Toiminnallisuudet</h2>
<br>

<h2>Blogien selaaminen</h2>
<li>
    <ul>Etusivu näyttää suosituimman (liketetyin) blogi. All blogs-sivulla julkaisuja voi hakea blogin kirjoittajan, otsikon tai sisällön mukaan.</ul>
</li>

<h2>Blogin toiminnot</h2>
<li>
    <ul>Kirjautuneet käyttäjät voivat lukea blogeja ja nähdä niiden kommentit sekä tykkäysten määrän. Käyttäjä voi myös tykätä ja kommentoida blogeja.</ul>
</li>

<h2>Käyttäjän omat toiminnot</h2>
<li>
    <ul>Profile-sivulta käyttäjä pystyy poistaa oman tilinsä mukaan lukien omat blogit, kommentit ja tykkäykset. Käyttäjä voi nähdä omat bloginsa ja blogit, joita käyttäjä on tykännyt</ul>
</li>
