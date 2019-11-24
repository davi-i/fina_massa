const determineSticky = () => {
  $('.sticky-top').each((i, el) => {
    const $nav = $(el),
      stickPoint = parseInt($nav.css('top')),
      currTop = el.getBoundingClientRect().top-parseInt($('html').css('font-size'))*1.5,
      isStuck = currTop <= stickPoint,
      scroll = $(window).scrollTop();
    $nav.toggleClass('py-lg-4', !isStuck);
    $(window).scrollTop(scroll);
  });
}
$(() => {
  determineSticky()
  $(window).on('resize scroll', $.debounce(25, () => {
    determineSticky();
  }));
});