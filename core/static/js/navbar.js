const determineSticky = () => {
  $('.sticky-top').each((i, el) => {
    const $nav = $(el),
      stickPoint = parseInt($nav.css('top')),
      currTop = el.getBoundingClientRect().top,
      isStuck = currTop <= stickPoint;
    $nav.toggleClass('py-lg-4', !isStuck);
    if (isStuck) $('html, body').scrollTop($nav.offset().top);
  });
}
$(() => {
  determineSticky()
  $(window).on('resize scroll', $.debounce(25, () => {
    determineSticky();
  }));
});