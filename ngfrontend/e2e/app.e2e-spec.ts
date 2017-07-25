import { NgfrontendPage } from './app.po';

describe('ngfrontend App', () => {
  let page: NgfrontendPage;

  beforeEach(() => {
    page = new NgfrontendPage();
  });

  it('should display welcome message', done => {
    page.navigateTo();
    page.getParagraphText()
      .then(msg => expect(msg).toEqual('Welcome to app!!'))
      .then(done, done.fail);
  });
});
