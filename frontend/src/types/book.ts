import type {Author} from "./author";
import type {Genre} from "./genre.ts";

export type Book = {
    id: number;
    eid: number;
    isbn: string;
    title: string;
    description: string;
    cover_url: string;
    content_url: string;
    pub_date: string;
    rating?: number;
    authors: Author[];
    genres: Genre[];
}