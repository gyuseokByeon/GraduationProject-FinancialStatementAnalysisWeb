module.exports = {
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      borderRadius: {
        xl: "1.5rem"
      },
      minHeight: {
        "50vh": "50vh",
        "75vh": "75vh"
      },
      extend: {
        backGroundImage: theme => ({
          'hero-pattern': "url('/img/hero-pattern.svg')",
         'footer-texture': "url('/img/footer-texture.png')",
        })
      }
    }
  },
  variants: {},
  plugins: []
};