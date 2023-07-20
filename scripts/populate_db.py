import sqlite3 as sql
import json
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@dataclass
class IO:
    input_dir: Path = field(default=Path(__file__).parents[1] / 'data' / 'nsf_grants')
    output_dir: Path = field(default=Path(__file__).parents[1] / 'data')
    db_name: Path = field(default=Path(__file__).parents[1] / 'data' / 'nsf.db')
    

@dataclass
class NSFIds:
    ids: list = field(default_factory=list)
    dates: list = field(default_factory=list)
    dateStarts: list = field(default_factory=list)
    dateEnds: list = field(default_factory=list)
    is_duplicates: list = field(default_factory=list)
    

@dataclass
class titles:
    ids: list = field(default_factory=list)
    titles: list = field(default_factory=list)


@dataclass
class abstracts:
    ids: list = field(default_factory=list)
    abstract: list = field(default_factory=list)
    
    
@dataclass
class pis:
    ids: list = field(default_factory=list)
    first_names: list = field(default_factory=list)
    last_names: list = field(default_factory=list)
    emails: list = field(default_factory=list)


def _load_json_files(directory: IO.input_dir) -> json:
    # load the json files
    files = [file for file in directory.glob('*.json')]
    # yield the json files
    for file in files:
        with open(file, 'r') as f:
            try:
                yield json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f'Error loading json file {file}: {e}')
                continue


def _insert_ids(ids: list,
                dates: list,
                dateStarts: list,
                dateEnds: list,
                is_duplicates: list,
                db_file: IO.db_name
    ) -> None:
    """Insert the ids into the database"""
    con = sql.connect(db_file)
    cur = con.cursor()
    # print the table names
    try:
        cur.executemany(f"""
            INSERT INTO nsf_id (id, date, dateStart, dateEnd, is_duplicate)
            VALUES (?, ?, ?, ?, ?)
        """, zip(ids, dates, dateStarts, dateEnds, is_duplicates)
        )
        con.commit()
    except sql.Error as e:
        logger.error(f'Error inserting ids into database: {e}')
    finally:
        con.close()


def _insert_titles(ids: list,
                   titles: list,
                   db_file: IO.db_name
    ) -> None:
    con = sql.connect(db_file)
    cur = con.cursor()
    try:
        cur.executemany(f"""
            INSERT INTO title (id, title)
            VALUES (?, ?)
        """, zip(ids, titles)
        )
        con.commit()
    except sql.Error as e:
        logger.error(f'Error inserting titles into database: {e}')
    finally:
        con.close()


def _insert_abstracts(ids: list,
                      abstracts: list,
                      db_file: IO.db_name
    ) -> None:
    con = sql.connect(db_file)
    cur = con.cursor()
    try:
        cur.executemany(f"""
                        INSERT INTO abstract (id, abstract)
                        VALUES (?, ?)
                        """, zip(ids, abstracts)
        )
        con.commit()
    except sql.Error as e:
        logger.error(f'Error inserting abstracts into database: {e}')
    finally:
        con.close()


def _insert_pis(ids: list,
                first_names: list,
                last_names: list,
                emails: list,
                db_file: IO.db_name
    ) -> None:
    con = sql.connect(db_file)
    cur = con.cursor()
    try:
        cur.executemany(f"""
                        INSERT INTO pi (id, first_name, last_name, email)
                        VALUES (?, ?, ?, ?)
                        """, zip(ids, first_names, last_names, emails)
        )
        con.commit()
    except sql.Error as e:
        logger.error(f'Error inserting pis into database: {e}')
    finally:
        con.close()


def main():
    data = IO()
    json_data = _load_json_files(data.input_dir)
    
    id_table = NSFIds()
    title_table = titles()
    abstract_table = abstracts()
    pis_table = pis()
    
    for json_file in json_data:
        # process the entries
        entries = json_file['response']['award']
        for entry in entries:
            # nsf_ids data
            id_table.ids.append(entry['id'] if 'id' in entry else None)
            id_table.dates.append(entry['date'] if 'date' in entry else None)
            id_table.dateStarts.append(entry['startDate'] if 'startDate' in entry else None)
            id_table.dateEnds.append(entry['expDate'] if 'expDate' in entry else None)
            id_table.is_duplicates.append(0 if 'is_duplicate' in entry else 1)
            
            # titles data
            title_table.ids.append(entry['id'] if 'id' in entry else None)
            title_table.titles.append(entry['title'] if 'title' in entry else None)
            
            # abstracts data
            abstract_table.ids.append(entry['id'] if 'id' in entry else None)
            abstract_table.abstract.append(" ".join(entry['abstractText'].split()) if 'abstractText' in entry else None)
            
            # pis data
            pis_table.ids.append(entry['id'] if 'id' in entry else None)
            pis_table.first_names.append(entry['piFirstName'] if 'piFirstName' in entry else None)
            pis_table.last_names.append(entry['piLastName'] if 'piLastName' in entry else None)
            pis_table.emails.append(entry['piEmail'] if 'piEmail' in entry else None)
            
        # insert the id data
        _insert_ids(id_table.ids,
                    id_table.dates,
                    id_table.dateStarts,
                    id_table.dateEnds,
                    id_table.is_duplicates,
                    data.db_name)
        
        # insert the title data
        _insert_titles(title_table.ids,
                       title_table.titles,
                       data.db_name)
        
        # insert the abstract data
        _insert_abstracts(abstract_table.ids,
                          abstract_table.abstract,
                          data.db_name)
        
        _insert_pis(pis_table.ids,
                    pis_table.first_names,
                    pis_table.last_names,
                    pis_table.emails,
                    data.db_name)
        
        # reset the lists
        id_table.ids.clear()
        id_table.dates.clear()
        id_table.dateStarts.clear()
        id_table.dateEnds.clear()
        id_table.is_duplicates.clear()
        
        title_table.ids.clear()
        title_table.titles.clear()
        
        abstract_table.ids.clear()
        abstract_table.abstract.clear()
        
        pis_table.ids.clear()
        pis_table.first_names.clear()
        pis_table.last_names.clear()
        pis_table.emails.clear()

if __name__ == '__main__':
    raise SystemExit(main())
