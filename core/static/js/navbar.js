const determineSticky = () => {
  $('.sticky-top').each((i, el) => {
    const $nav = $(el),
      stickPoint = parseInt($nav.css('top')),
      currTop = el.getBoundingClientRect().top-parseInt($('html').css('font-size'))*1.5,
      isStuck = currTop <= stickPoint;
    $nav.toggleClass('py-lg-4', !isStuck);
  });
}
$(() => {
  determineSticky()
  $(window).on('resize scroll', $.debounce(25, () => {
    determineSticky();
  }));
});