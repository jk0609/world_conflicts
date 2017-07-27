export class Article {
  constructor(
    public title: string,
    public summary: string,
    public url: string,
    public lat: number,
    public lon: number,
    public city: string,
    public country: string
  ){}
}
